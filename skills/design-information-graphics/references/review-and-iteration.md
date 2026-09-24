# Review and Iteration

After rendering, check fidelity, integrity, narrative, hierarchy, annotation accuracy, spacing, clipping, and collection consistency. Repair low-risk presentation defects automatically. Ask before changing the message, audience, comparison, scale interpretation, contract, or narrative role. Present the draft with a brief rationale and ask one focused question about what feels wrong or incomplete.

For external feedback, load the brief, contract, source, metadata, current outputs, and feedback history. Split comments into atomic requests and classify each as accepted, clarification needed, conflicting, changing the objective, upstream data work, potentially misleading, or rejected with rationale. Do not treat feedback as automatically correct.

Keep `graphic_id` stable and increment `version`. Never silently overwrite prior versions. Record what changed, why, which feedback prompted it, whether the message or contract changed, and the evidence fingerprint.

Use the lifecycle `draft -> creator-review -> release-candidate -> external-review -> revision -> approved`. New feedback or data may reopen an approved graphic.
