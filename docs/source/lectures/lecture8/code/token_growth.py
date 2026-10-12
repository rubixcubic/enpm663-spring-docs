"""L8: how input tokens and cost grow with the number of loop steps.

Every number below is an assumption chosen for this example, not a
measurement and not a provider's price. A team reads real token counts
from the API's usage fields and real prices from the provider's page.

Run: python3 token_growth.py
"""

FIXED = 2000      # sent on every call: system prompt, tools, state
PER_STEP = 250    # added by each earlier step: a tool call + result
OUT = 100         # output tokens per ReAct call
PLAN_OUT = 40     # output tokens per step of a written plan
PRICE_IN = 2.0    # dollars per million input tokens
PRICE_OUT = 10.0  # dollars per million output tokens


def react(n):
    """n calls; call k re-sends FIXED plus the k - 1 earlier steps."""
    inputs = [FIXED + (k - 1) * PER_STEP for k in range(1, n + 1)]
    return sum(inputs), n * OUT, inputs[-1]


def plan_execute(n, replans=1):
    """One call writes an n-step plan; each replan is one more call.

    A replan sends the current state read from ROS, not the history,
    so each call sends FIXED tokens.
    """
    calls = 1 + replans
    return calls * FIXED, calls * n * PLAN_OUT


def cost(tokens_in, tokens_out):
    return (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1e6


if __name__ == "__main__":
    print("ReAct, one call per step")
    print(f"{'steps':>5} {'last call':>9} {'input':>7} {'output':>6}"
          f" {'cost $':>7}")
    for n in (5, 10, 20, 40):
        t_in, t_out, last = react(n)
        print(f"{n:>5} {last:>9} {t_in:>7} {t_out:>6}"
              f" {cost(t_in, t_out):>7.4f}")
    print("Plan-and-execute, one plan and one replan")
    print(f"{'steps':>5} {'calls':>9} {'input':>7} {'output':>6}"
          f" {'cost $':>7}")
    for n in (5, 10, 20, 40):
        t_in, t_out = plan_execute(n)
        print(f"{n:>5} {2:>9} {t_in:>7} {t_out:>6}"
              f" {cost(t_in, t_out):>7.4f}")
