// Custom tool: plan_exit - signals completion of planning phase and spins up orchestrator session
import { type Plugin, tool } from "@opencode-ai/plugin";
import * as fs from "fs";
import * as path from "path";
import { parseModel } from "../../utilities/shared/providers";

const PLAN_STATE_DIR = ".serena";
const PLAN_STATE_FILE = "plan_state.json";

function ensurePlanExists(planPath: string): void {
  if (!fs.existsSync(planPath)) {
    throw new Error(`Plan file not found at ${planPath}`);
  }
}

function writePlanState(
  directory: string,
  data: Record<string, unknown>,
): void {
  const dir = path.join(directory, PLAN_STATE_DIR);
  const filePath = path.join(dir, PLAN_STATE_FILE);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2), "utf-8");
}

export const PlanExitPlugin: Plugin = async ({ client }) => {
  return {
    tool: {
      plan_exit: tool({
        description:
          "Use when the plan is ready and you want to start a fresh orchestrator session. MUST ensure the plan exists before calling.",
        args: {
          plan_path: tool.schema
            .string()
            .describe("Absolute path to the plan file on disk."),
          orchestrator_agent: tool.schema
            .string()
            .optional()
            .describe("Orchestrator agent to use for the new session."),
          orchestrator_model: tool.schema
            .string()
            .optional()
            .describe("Optional provider/model for the orchestrator session."),
          build_agent: tool.schema
            .string()
            .optional()
            .describe("Deprecated alias for orchestrator_agent."),
          build_model: tool.schema
            .string()
            .optional()
            .describe("Deprecated alias for orchestrator_model."),
          session_title: tool.schema
            .string()
            .optional()
            .describe("Optional title for the new orchestrator session."),
        },
        async execute(args, context) {
          const { sessionID, directory } = context;
          const orchestratorAgent =
            args.orchestrator_agent ?? args.build_agent ?? "Orchestrator (Custom)";
          const title =
            args.session_title ??
            `orchestrator:${path.basename(args.plan_path)}:${Date.now()}`;

          ensurePlanExists(args.plan_path);

          const { data: session } = await client.session.create({
            body: { title, parentID: sessionID },
          });

          const orchestratorSessionID = session?.id;
          if (!orchestratorSessionID) {
            throw new Error("Failed to create orchestrator session.");
          }

          writePlanState(directory, {
            plan_path: args.plan_path,
            approved_from_session: sessionID,
            orchestrator_session_id: orchestratorSessionID,
            orchestrator_session_title: title,
            approved_at: new Date().toISOString(),
          });

          const requestedModel = args.orchestrator_model ?? args.build_model;
          const modelSpec = parseModel(requestedModel);
          if (requestedModel && !modelSpec) {
            throw new Error(
              "Invalid orchestrator model. Use provider/model (e.g. opencode/big-pickle).",
            );
          }

          await client.session.promptAsync({
            path: { id: orchestratorSessionID },
            body: {
              agent: orchestratorAgent,
              model: modelSpec,
              parts: [
                {
                  type: "text",
                  text: [
                    "You are now in orchestrator mode.",
                    `Review the plan at ${args.plan_path}.`,
                    "Follow the plan exactly. If you need changes, request them before editing.",
                  ].join("\n"),
                },
              ],
            },
          });

          return [
            "[plan_exit] Orchestrator session created.",
            `Session ID: ${orchestratorSessionID}`,
            `Title: ${title}`,
            `Plan: ${args.plan_path}`,
            "Next: switch to the new session to continue orchestrator execution.",
          ].join("\n");
        },
      }),
    },
  };
};
