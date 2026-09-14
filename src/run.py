"""L1 entrypoint. Dispatches domain mappers, writes reports.

Profile selection:
  1. `--profile <name>` CLI arg (sets CONVERTER_PROFILE env var)
  2. `CONVERTER_PROFILE` env var
  3. default: `thailand`

Usage:
  python -m converter.src.run                 # default profile
  python -m converter.src.run --profile foo   # select profile 'foo'
  python -m converter.src.run org security    # run subset of domains
"""
from __future__ import annotations

import argparse
import os
import sys


def _apply_profile_arg() -> list[str]:
    """Pre-parse --profile before importing anything that reads the profile."""
    ap = argparse.ArgumentParser(add_help=False)
    ap.add_argument("--profile", default=None)
    known, rest = ap.parse_known_args(sys.argv[1:])
    if known.profile:
        os.environ["CONVERTER_PROFILE"] = known.profile
    return rest


_rest = _apply_profile_arg()

# Imports below trigger profile loading — must happen after env var set.
from .common import Coverage, write_report, write_unmapped  # noqa: E402
from .mappers import accounts as accounts_mapper  # noqa: E402
from .mappers import customizations as customizations_mapper  # noqa: E402
from .mappers import globalcfg as global_mapper  # noqa: E402
from .mappers import iam as iam_mapper  # noqa: E402
from .mappers import network as network_mapper  # noqa: E402
from .mappers import org as org_mapper  # noqa: E402
from .mappers import security as security_mapper  # noqa: E402
from . import profile as _profile  # noqa: E402


# Ordering matters: security must run before globalcfg (session-manager deferral).
DOMAINS = {
    "org": org_mapper.build_organization_config,
    "security": security_mapper.build_security_config,
    "iam": iam_mapper.build_iam_config,
    "global": global_mapper.build_global_config,
    "network": network_mapper.build_network_config,
    "accounts": accounts_mapper.build_accounts_config,
    "replacements": accounts_mapper.build_replacements_config,
}


def main(rest: list[str]) -> int:
    domains = rest or list(DOMAINS)
    print(f"[L1] profile={_profile.PROFILE_NAME}  out={_profile.OUT_DIR}")
    for d in domains:
        if d not in DOMAINS:
            print(f"unknown domain: {d}", file=sys.stderr)
            return 2
        print(f"[L1] running domain: {d}")
        cov: Coverage = DOMAINS[d]()
        write_report(d, cov)
        write_unmapped(d, cov)
        print(f"  mapped={len(cov.mapped)} unmapped={len(cov.unmapped)} dropped={len(cov.dropped)}")

    # Aggregator pass — writes customizations-config.yaml if any mapper registered entries
    print("[L1] aggregating customizations")
    cust_cov = Coverage()
    customizations_mapper.build_customizations_config(cust_cov)
    write_report("customizations", cust_cov)
    return 0


if __name__ == "__main__":
    sys.exit(main(_rest))
