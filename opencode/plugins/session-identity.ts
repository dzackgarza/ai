type TextPart = {
  text?: string;
  type?: string;
};

type MessageInfo = {
  agent?: string;
  model?: {
    modelID?: string;
    providerID?: string;
  };
  role?: string;
};

type SessionMessage = {
  info?: MessageInfo;
  parts?: TextPart[];
};

export type SessionIdentity = {
  agent: string;
  model: {
    modelID: string;
    providerID: string;
  };
};

export const MISSING_SESSION_IDENTITY_MESSAGE =
  'No prior non-empty user message with agent/model found in session history';

function flattenText(parts: TextPart[] | undefined): string {
  if (!parts) return '';

  return parts
    .filter(
      (part): part is TextPart & { text: string; type: 'text' } =>
        part.type === 'text' && typeof part.text === 'string' && part.text.trim().length > 0,
    )
    .map((part) => part.text.trim())
    .join('\n\n');
}

export function observedSessionIdentity(
  messages: SessionMessage[] | undefined,
): SessionIdentity | null {
  if (!messages) return null;

  for (const message of [...messages].reverse()) {
    const info = message.info;
    if (!info || info.role !== 'user') continue;
    if (!flattenText(message.parts)) continue;

    const agent = info.agent;
    const providerID = info.model?.providerID;
    const modelID = info.model?.modelID;

    if (!agent || !providerID || !modelID) continue;

    return {
      agent,
      model: {
        modelID,
        providerID,
      },
    };
  }

  return null;
}
