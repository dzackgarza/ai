// Custom tool: write_plan - writes a plan document to .serena/plans/
import { type Plugin, tool } from "@opencode-ai/plugin";

function generateSlug(content: string): string {
  // Extract first meaningful word from content (skip markdown headers)
  const lines = content
    .split("\n")
    .filter((l) => l.trim() && !l.startsWith("#"));
  if (lines.length === 0) return "plan";

  const firstLine = lines[0].trim();
  // Take first word, lowercase, remove special chars
  const word =
    firstLine
      .split(/\s+/)[0]
      ?.toLowerCase()
      .replace(/[^a-z0-9]/g, "") || "plan";
  return word.slice(0, 20); // Limit slug length
}

function formatDateTime(): string {
  const now = new Date();
  const yyyy = now.getFullYear();
  const mm = String(now.getMonth() + 1).padStart(2, "0");
  const dd = String(now.getDate()).padStart(2, "0");
  const hh = String(now.getHours()).padStart(2, "0");
  const min = String(now.getMinutes()).padStart(2, "0");
  const ss = String(now.getSeconds()).padStart(2, "0");
  return `${yyyy}-${mm}-${dd}-${hh}${min}${ss}`;
}

export const WritePlanPlugin: Plugin = async (ctx) => {
  // Capture $ shell from plugin context
  const shell = ctx.$;

  return {
    tool: {
      write_plan: tool({
        description:
          "Use when the planning phase is complete and the plan must be committed to disk. MUST be called before plan_exit.",
        args: {
          plan: tool.schema.string(),
        },
        async execute(args, context) {
          const { directory } = context;
          const slug = generateSlug(args.plan);
          const timestamp = formatDateTime();
          const filename = `${slug}-${timestamp}.md`;
          const filepath = `${directory}/.serena/plans/${filename}`;

          // Ensure directory exists using $ shell
          await shell`mkdir -p ${directory}/.serena/plans`;

          // Write file using printf to escape content properly
          const escapedPlan = args.plan.replace(/'/g, "'\"'\"'");
          await shell`printf '%s' '${escapedPlan}' > ${filepath}`;

          return `Plan written to: ${filepath}`;
        },
      }),
    },
  };
};
