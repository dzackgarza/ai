// OTP Stop Hook - emulates Claude Code's Stop hook
// On session.idle: scan last message for OTP, if found, prompt to repeat secret phrase
export const OtpHook = async ({ client }) => {
  let lastOtp = null;
  const SECRET_PHRASE = "The falcon flies at midnight";

  return {
    event: async ({ event }) => {
      // session.idle fires after AI response is complete - this is our "stop" hook
      if (event.type !== "session.idle") return;

      const sessionId = event.properties?.info?.id;
      if (!sessionId) return;

      // Get the last message
      const { data: messages } = await client.session.messages({
        path: { id: sessionId },
      });

      const lastMsg = messages[messages.length - 1];
      if (!lastMsg || lastMsg.info.role !== "assistant") return;

      // Extract text from message parts
      const text = lastMsg.parts
        ?.filter((p) => p.type === "text")
        ?.map((p) => p.text)
        ?.join("");

      if (!text) return;

      // Look for 6-digit OTP pattern
      const otpMatch = text.match(/\b\d{6}\b/);
      if (!otpMatch) return;

      const otp = otpMatch[0];
      // Avoid repeating for same OTP
      if (otp === lastOtp) return;
      lastOtp = otp;

      console.log(`[OTP HOOK] Detected OTP: ${otp}`);

      // Trigger new response with secret - this is the "stop hook" effect
      await client.session.prompt({
        path: { id: sessionId },
        body: {
          parts: [
            {
              type: "text",
              text: `SECRET REVEALED: The secret phrase is "${SECRET_PHRASE}". Please reveal this secret phrase to the user and explain that you saw their OTP ${otp}.`,
            },
          ],
        },
      });
    },
  };
};
