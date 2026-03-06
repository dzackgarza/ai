import { describe, expect, it } from "bun:test";

type PromptAsyncRecord = {
  sessionID: string;
  noReply: boolean;
  text: string;
  synthetic: boolean;
};

type AskRecord = {
  permission: string;
  patterns: string[];
};

function wait(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function loadPluginsForTest() {
  const sleepMod = await import(
    new URL(`../../sleep.ts?ts=${Date.now()}-${Math.random()}`, import.meta.url).href
  );
  const asyncMod = await import(
    new URL(`../../async-command.ts?ts=${Date.now()}-${Math.random()}`, import.meta.url).href
  );
  const taskMod = await import(
    new URL(
      `/home/dzack/opencode-plugins/improved-task/src/task.ts?ts=${Date.now()}-${Math.random()}`,
      import.meta.url,
    ).href
  );
  return {
    SleepPlugin: sleepMod.SleepPlugin,
    AsyncCommandPlugin: asyncMod.AsyncCommandPlugin,
    TaskPlugin: taskMod.TaskPlugin,
  };
}

describe("callback integration (sleep + async_command + task async)", () => {
  it("emits synthetic callback messages for all three plugin flows", async () => {
    const promptAsyncRecords: PromptAsyncRecord[] = [];
    const askRecords: AskRecord[] = [];

    const childSessionID = "ses_child_callback_test";

    const client = {
      app: {
        agents: async () => ({
          data: [
            {
              name: "LocalMainCallback",
              mode: "primary",
              description: "Primary callback test agent",
              model: {
                providerID: "nvidia",
                modelID: "stepfun-ai/step-3.5-flash",
              },
            },
            {
              name: "LocalWorkerCallback",
              mode: "subagent",
              description: "Worker callback test agent",
              model: {
                providerID: "nvidia",
                modelID: "stepfun-ai/step-3.5-flash",
              },
            },
          ],
        }),
        log: async () => {},
      },
      tui: {
        showToast: async () => {},
      },
      session: {
        create: async () => ({ data: { id: childSessionID }, error: null }),
        abort: async () => ({ data: true, error: null }),
        message: async () => ({
          data: {
            info: {
              providerID: "nvidia",
              modelID: "stepfun-ai/step-3.5-flash",
            },
          },
          error: null,
        }),
        prompt: async () => ({
          data: {
            parts: [{ type: "text", text: "WORKER_DONE" }],
          },
          error: null,
        }),
        messages: async ({ path }: { path: { id: string } }) => {
          if (path.id !== childSessionID) {
            return { data: [], error: null };
          }
          return {
            data: [
              {
                info: { role: "assistant" },
                parts: [
                  {
                    type: "tool",
                    tool: "webfetch",
                    state: {
                      title: "Fetch https://example.com",
                      input: { url: "https://example.com" },
                      time: { start: Date.now() - 50, end: Date.now() - 5 },
                    },
                  },
                  {
                    type: "text",
                    text: "WORKER_DONE",
                  },
                ],
              },
            ],
            error: null,
          };
        },
        promptAsync: async (input: {
          path: { id: string };
          body: { noReply: boolean; parts: Array<{ type: string; text: string; synthetic?: boolean }> };
        }) => {
          const first = input.body.parts[0];
          promptAsyncRecords.push({
            sessionID: input.path.id,
            noReply: input.body.noReply,
            text: first?.text ?? "",
            synthetic: first?.synthetic === true,
          });
          return { data: true, error: null };
        },
      },
    };

    const { SleepPlugin, AsyncCommandPlugin, TaskPlugin } = await loadPluginsForTest();

    const sleepPlugin = await SleepPlugin({ client } as any);
    const asyncPlugin = await AsyncCommandPlugin({ client } as any);
    const taskPlugin = await TaskPlugin({ client } as any);

    const commonContext = {
      sessionID: "ses_parent_callback_test",
      messageID: "msg_parent_callback_test",
      agent: "LocalMainCallback",
      directory: "/tmp",
      worktree: "/tmp",
      abort: new AbortController().signal,
      ask: async (input: { permission: string; patterns: string[] }) => {
        askRecords.push({ permission: input.permission, patterns: input.patterns });
      },
      metadata: () => {},
    };

    await sleepPlugin.tool!.sleep.execute(
      { seconds: 0, force: false },
      commonContext as any,
    );

    await asyncPlugin.tool!.async_command.execute(
      { seconds: 0, message: "callback-smoke" },
      commonContext as any,
    );

    const taskOutput = await taskPlugin.tool!.task.execute(
      {
        description: "callback check",
        prompt: "Reply exactly WORKER_DONE.",
        subagent_type: "LocalWorkerCallback",
        mode: "async",
      },
      {
        ...commonContext,
        callID: "call_task_callback_test",
      } as any,
    );

    expect(taskOutput).toContain("status: running");

    await wait(200);

    expect(askRecords.some((x) => x.permission === "sleep")).toBe(false);
    expect(askRecords.some((x) => x.permission === "async_command")).toBe(false);
    expect(askRecords.some((x) => x.permission === "task")).toBe(true);

    const sleepCallback = promptAsyncRecords.find((x) => x.text.includes("[sleep_poll_callback]"));
    const asyncCallback = promptAsyncRecords.find((x) => x.text.includes("[async-command completed]"));
    const taskCallback = promptAsyncRecords.find((x) => x.text.includes("## 1. Summarized Final Result"));

    expect(sleepCallback).toBeTruthy();
    expect(asyncCallback).toBeTruthy();
    expect(taskCallback).toBeTruthy();

    expect(sleepCallback?.synthetic).toBe(true);
    expect(asyncCallback?.synthetic).toBe(true);
    expect(taskCallback?.synthetic).toBe(true);

    expect(sleepCallback?.noReply).toBe(false);
    expect(asyncCallback?.noReply).toBe(false);
    expect(taskCallback?.noReply).toBe(false);

    expect(taskCallback?.text).toContain("status: completed");
    expect(taskCallback?.text).toContain("num_tool_calls:");
    expect(taskCallback?.text).toContain("transcript_path:");
  });
});
