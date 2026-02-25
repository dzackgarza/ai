; Z3 proof for "Heart of the Empire"
; Run: z3 proof/proof.smt2

(set-logic ALL)

(declare-datatypes () ((Suspect Blackwood Violet Elm Scarlett Green)))
(declare-const culprit Suspect)

; Abbreviations for "who did what" (modeled as total functions returning a suspect)
(declare-fun case_opener_pre_blackout () Suspect)
(declare-fun replica_signout_actor () Suspect)
(declare-fun vault_access_actor () Suspect)

; Evidence encoding (directly from case files)
;
; - `GRN-1` is the curator key issued to Mr. Green, and it opened the ballroom case at 19:58:46
;   (`case/locations/ballroom/lock-audit.txt`)
; - Guard observed Mr. Green unlock/open/close/re-lock in that minute
;   (`case/locations/ballroom/scene-report.md`)
(assert (= case_opener_pre_blackout Green))

; - Replica WS-02 / Batch 14 signed out by curator badge GRN, and only curator can sign out
;   (`case/locations/museum/workshop-log.md`)
(assert (= replica_signout_actor Green))

; - Vault accessed only by curator badge GRN in 20:05..20:20, with biometric requirement
;   (`case/locations/museum/security-log.txt`)
(assert (= vault_access_actor Green))

; Culprit must satisfy all these roles.
(assert (= culprit case_opener_pre_blackout))
(assert (= culprit replica_signout_actor))
(assert (= culprit vault_access_actor))

; Existence (who is the culprit?)
(check-sat)
(get-model)

; Uniqueness: no other suspect can be the culprit.
(push)
(assert (not (= culprit Green)))
(check-sat)
(pop)
