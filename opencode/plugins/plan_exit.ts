import { isPluginEnabled } from "./plugins_config";
// Custom tool: plan_exit - signals completion of planning phase and spins up build session
import { type Plugin, tool } from "@opencode-ai/plugin";
import * as fs from "fs";
import * as path from "path";

const PLAN_STATE_DIR = ".serena";
const PLAN_STATE_FILE = "plan_state.json";

function parseModel(
  model?: string,
): { providerID: string; modelID: string } | undefined {
  if (!model) return undefined;
  const [providerID, ...rest] = model.split("/");
  if (!providerID || rest.length === 0) return undefined;
  return { providerID, modelID: rest.join("/") };
}

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
  if (!isPluginEnabled("plan_exit")) return {};

  return {
    tool: {
      plan_exit: tool({
        description:
          "Use when the plan is ready and you want to start a fresh build session. MUST ensure the plan exists before calling.",
        args: {
          plan_path: tool.schema
            .string()
            .describe("Absolute path to the plan file on disk."),
          build_agent: tool.schema
            .string()
            .optional()
            .describe("Build agent to use for the new session."),
          build_model: tool.schema
            .string()
            .optional()
            .describe("Optional provider/model for the build session."),
          session_title: tool.schema
            .string()
            .optional()
            .describe("Optional title for the new build session."),
        },
        async execute(args, context) {
          const { sessionID, directory } = context;
          const buildAgent = args.build_agent ?? "Build";
          const title =
            args.session_title ??
            `build:${path.basename(args.plan_path)}:${Date.now()}`;

          ensurePlanExists(args.plan_path);

          const { data: session } = await client.session.create({
            body: { title, parentID: sessionID },
          });

          const buildSessionID = session?.id;
          if (!buildSessionID) {
            throw new Error("Failed to create build session.");
          }

          writePlanState(directory, {
            plan_path: args.plan_path,
            approved_from_session: sessionID,
            build_session_id: buildSessionID,
            build_session_title: title,
            approved_at: new Date().toISOString(),
          });

          const modelSpec = parseModel(args.build_model);
          if (args.build_model && !modelSpec) {
            throw new Error(
              "Invalid build_model. Use provider/model (e.g. opencode/big-pickle).",
            );
          }

          await client.session.promptAsync({
            path: { id: buildSessionID },
            body: {
              agent: buildAgent,
              model: modelSpec,
              parts: [
                {
                  type: "text",
                  text: [
                    "You are now in build mode.",
                    `Review the plan at ${args.plan_path}.`,
                    "Follow the plan exactly. If you need changes, request them before editing.",
                  ].join("\n"),
                },
              ],
            },
          });

          return [
            "[plan_exit] Build session created.",
            `Session ID: ${buildSessionID}`,
            `Title: ${title}`,
            `Plan: ${args.plan_path}`,
            "Next: switch to the new session to continue build execution.",
          ].join("\n");
        },
      }),
    },
  };
};
