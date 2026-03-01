#!/usr/bin/env python3
"""
Langfuse-based OpenCode transcript reconstruction script.
Replaces the need for 'opencode export' by directly fetching session data from Langfuse API.
"""

import json
import sys
from typing import Dict, Any, Optional
import os


class LangfuseTranscriptParser:
    """Parse OpenCode transcripts directly from Langfuse session data."""

    def __init__(self, langfuse_host: str, public_key: str, secret_key: str):
        """Initialize Langfuse client configuration."""
        self.host = langfuse_host
        self.public_key = public_key
        self.secret_key = secret_key

def get_session_data(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Fetch session data from Langfuse API."""
        try:
            url = f"{self.host}/api/public/sessions/{session_id}"
            auth = base64.b64encode(f"{self.public_key}:{self.secret_key}".encode()).decode()
            
            headers = {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json"
            }
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching session {session_id}: {e}")
            return None

    def reconstruct_opencode_transcript(self, session_data: Dict[str, Any]) -> str:
        """Reconstruct transcript format matching opencode export structure."""

        # Extract session info
        session_body = session_data.get("body", {})
        session_id = session_body.get("id", "unknown")
        created_at = session_body.get("createdAt", "unknown")

        # Build the opencode-style transcript structure
        transcript = {
            "info": {
                "id": session_id,
                "title": f"Langfuse Session: {session_id}",
                "createdAt": created_at,
                "source": "langfuse",
            },
            "messages": [],
        }

        # Process traces as messages
        traces = session_body.get("traces", [])
        for i, trace in enumerate(traces):
            message = self._convert_trace_to_message(trace, i)
            if message:
                transcript["messages"].append(message)

        return json.dumps(transcript, indent=2, ensure_ascii=False)

    def _convert_trace_to_message(
        self, trace: Trace, index: int
    ) -> Optional[Dict[str, Any]]:
        """Convert a Langfuse trace to opencode message format."""

        # Basic trace info
        trace_id = trace.get("id", f"trace_{index}")
        trace_name = trace.get("name", f"Trace {index}")

        # Extract input/output messages
        input_data = trace.get("input", {})
        output_data = trace.get("output", {})

        # Build parts array
        parts = []

        # Add input as user message if it contains messages
        if "messages" in input_data:
            for msg in input_data["messages"]:
                if msg.get("role") == "user":
                    parts.append({"type": "text", "text": msg.get("content", "")})
                elif msg.get("role") == "system":
                    # System prompt can be included as reasoning
                    parts.append(
                        {
                            "type": "reasoning",
                            "text": f"System: {msg.get('content', '')}",
                        }
                    )

        # Add output as assistant message
        if output_data:
            if isinstance(output_data, str):
                parts.append({"type": "text", "text": output_data})
            elif isinstance(output_data, dict):
                # Handle structured output
                if "content" in output_data:
                    parts.append({"type": "text", "text": output_data["content"]})
                # Add other fields as needed
                for key, value in output_data.items():
                    if key != "content":
                        parts.append(
                            {
                                "type": "reasoning",
                                "text": f"[Output {key}]: {str(value)[:200]}{'...' if len(str(value)) > 200 else ''}",
                            }
                        )

        # Skip if no meaningful content
        if not parts:
            return None

        return {
            "info": {
                "role": "assistant" if index % 2 == 1 else "user",
                "trace_id": trace_id,
                "name": trace_name,
            },
            "parts": parts,
        }

    def parse_session(self, session_id: str) -> str:
        """Main parsing method - fetch and reconstruct transcript."""
        print(f"Fetching Langfuse session: {session_id}")

        session_data = self.get_session_data(session_id)
        if not session_data:
            print(f"Error: Could not fetch session {session_id}")
            return ""

        print(f"Reconstructing transcript for session {session_id}")
        return self.reconstruct_opencode_transcript(session_data)


def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python parse_langfuse_opencode.py <session-id>")
        print("Example: python parse_langfuse_opencode.py ses_1234567890abcdef")
        sys.exit(1)

    session_id = sys.argv[1]

    # Get Langfuse credentials from environment
    langfuse_host = os.getenv("LANGFUSE_HOST")
    public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
    secret_key = os.getenv("LANGFUSE_SECRET_KEY")

    if not all([langfuse_host, public_key, secret_key]):
        print(
            "Error: LANGFUSE_HOST, LANGFUSE_PUBLIC_KEY, and LANGFUSE_SECRET_KEY environment variables required"
        )
        print("Example:")
        print("  export LANGFUSE_HOST=https://cloud.langfuse.com")
        print("  export LANGFUSE_PUBLIC_KEY=pk-lf-...")
        print("  export LANGFUSE_SECRET_KEY=sk-lf-...")
        sys.exit(1)

    # Create parser and process session
    parser = LangfuseTranscriptParser(langfuse_host, public_key, secret_key)
    transcript = parser.parse_session(session_id)

    if transcript:
        print(transcript)
    else:
        print("Error: Failed to generate transcript")
        sys.exit(1)


if __name__ == "__main__":
    main()
