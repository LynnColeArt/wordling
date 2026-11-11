# Independent proofreading interruption source review

Approved 18d2dcbf08323bb48881eecf3eb3a3b6f7a725a1 over a06b75841940843897221b7f912dba7fd8395dfa. Only the editor proofreading session and its existing public live test change. The reviewer did not author the implementation.

Stopped original captures distinguish Word F1 returning straight to Check, Page F1 showing the partial count and returning to Check on acknowledgement, and Document F1 preserving its existing partial-count exit to editing. The two reducer changes match those phase transitions. The public regression exercises all three with native bytes and caret retained. Fresh independent proof race tests and scoped diff validation passed. Intake this exact reviewed source before the final terminal proof workflow.
