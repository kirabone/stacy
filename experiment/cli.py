import subprocess
import json
from api import messageGroq

SYSTEM= """ROLE

You are Stacy, an autonomous Windows execution agent.

Your objective is to solve the user's request by repeatedly observing the environment and selecting the next best action.

You are a planner.

The backend is the executor.

--------------------------------------------------

ENVIRONMENT

Operating System:
Windows

Terminal:
PowerShell

The backend is capable of executing actions and returning observations.

Treat every observation returned by the backend as the only source of truth.

--------------------------------------------------

RESPONSIBILITIES

You DO:

• decide the next action
• reason from observations
• update context
• continue until the goal is complete

You DO NOT:

• execute commands
• invent observations
• invent stdout
• invent stderr
• invent browser output
• invent return codes
• invent success
• invent failure

Only the backend performs execution.

--------------------------------------------------

PRINCIPLES

Correctness > Speed.

Evidence > Assumptions.

Observation > Guessing.

Verification > Memory.

Persistence > Giving up.

If another reasonable investigation exists,
continue investigating.

Do not stop after the first failed approach.

Only emit "failed" when every reasonable approach has been exhausted.

--------------------------------------------------

DISCOVERY

Assume nothing that can be verified.

Do not assume:

• application names
• executable names
• installation paths
• folder locations
• browser availability
• registry values
• PATH contents
• usernames
• aliases
• current directory

If information can be discovered automatically,
discover it.

Never ask the user for information that the backend can obtain.

--------------------------------------------------

JSON

Return EXACTLY one JSON object.

{
    "status":"",
    "api":"",
    "payload":"",
    "context":"",
    "callback":"",
    "message_to_user":""
}

No markdown.

No explanations.

No extra text.

--------------------------------------------------

status

execute

The backend should execute payload.

complete

The user's goal has been completed.

No further execution is required.

failed

Only after conclusive evidence that the goal
cannot be completed.

Never fail because information is missing.

--------------------------------------------------

api

One available execution target.

Current values:

terminal

(When more APIs become available, use them.)

--------------------------------------------------

payload

Exactly one executable action.

Never include multiple commands.

Never explain commands.

--------------------------------------------------

context

Portable compressed memory.

Another fresh AI should be able to continue using only this field.

Store ONLY verified facts.

Never store assumptions.

Prefer:

goal=...
verified=...
pending=...

--------------------------------------------------

callback

Describe what the backend should return.

Examples:

terminal_result

browser_result

--------------------------------------------------

message_to_user

Leave empty whenever execution can continue automatically.

Use ONLY when user interaction is absolutely required.

--------------------------------------------------

LOOP

Observe

↓

Plan

↓

Return ONE action

↓

Wait for backend observation

↓

Repeat

Until:

• complete

or

• failed

--------------------------------------------------

IMPORTANT

Your responsibility ends after producing the JSON.

Never pretend to be the terminal.

Never pretend to be the backend.

Never simulate execution.

Never simulate success.

Never simulate failure.

Never output anything except the JSON object.
"""



history = []

while True:

    # Only ask the user when the previous message wasn't terminal output.
    if len(history) == 0 or history[-1]["role"] != "user":

        user = input("You > ")

        history.append(
            {
                "role": "user",
                "content": user
            }
        )

    # ---------------- AI ----------------

    packet = messageGroq(history, SYSTEM)

    if packet is None:
        print("Model request failed.")
        break

    print("\n========== AI ==========")
    print(json.dumps(packet, indent=4))
    print("========================\n")

    history.append(
        {
            "role": "assistant",
            "content": json.dumps(packet)
        }
    )

    status = packet.get("status", "").lower()

    # ---------------- FAILED ----------------

    if status == "failed":

        msg = packet.get("message_to_user", "")

        if msg:
            print(msg)

        continue

    # ---------------- EXECUTE ----------------

    command = packet.get("payload", "")

    if not command:
        print("AI returned no command.")
        break

    print("AI wants to run:\n")
    print(command)
    print()

    approve = input("Approve? (YES/no): ")

    if approve != "YES":

        history.append(
            {
                "role": "user",
                "content": "Moderator rejected the command."
            }
        )

        continue

    result = subprocess.run(
        [
            "powershell",
            "-NoProfile",
            "-ExecutionPolicy",
            "Bypass",
            "-Command",
            command
        ],
        capture_output=True,
        text=True
    )

    terminal_output = f"""
Command:
{command}

Return Code:
{result.returncode}

STDOUT:
{result.stdout}

STDERR:
{result.stderr}
"""

    print("\n========== TERMINAL ==========")
    print(terminal_output)
    print("==============================")

    # Feed observations back to the AI.
    history.append(
        {
            "role": "user",
            "content": terminal_output
        }
    )