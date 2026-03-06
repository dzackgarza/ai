export type CommandExecutionResult = {
  stdoutText: string;
  stderrText: string;
  exitCode: number;
};

export type RunCommand = (
  args: string[],
  timeoutMs?: number,
) => Promise<CommandExecutionResult>;

export type WebFetchHandlerInput = {
  url: URL;
};

export type WebFetchHandlerResult = {
  routeName: string;
  sourceUrl: string;
  content: string;
};

export type WebFetchDomainHandler = {
  name: string;
  domains: readonly string[];
  handle: (input: WebFetchHandlerInput) => Promise<WebFetchHandlerResult>;
};

export function hostMatchesDomain(hostname: string, domain: string): boolean {
  return hostname === domain || hostname.endsWith(`.${domain}`);
}
