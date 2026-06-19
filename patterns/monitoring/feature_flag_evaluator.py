class FeatureFlagEvaluator:
    def __init__(self):
        self.flags = {}

    def add_flag(
        self,
        flag_name: str,
        enabled: bool,
        allowed_users: list[str] | None = None,
        allowed_groups: list[str] | None = None,
    ) -> None:
        self.flags[flag_name] = {
            "enabled": enabled,
            "allowed_users": set(allowed_users or []),
            "allowed_groups": set(allowed_groups or []),
        }

    def is_enabled(
        self,
        flag_name: str,
        user: str,
        groups: list[str],
    ) -> bool:
        if flag_name not in self.flags:
            return False

        flag_info = self.flags[flag_name]
        flag_enabled = flag_info.get("enabled", False)
        allowed_users = flag_info.get("allowed_users", set())
        allowed_groups = flag_info.get("allowed_groups", set())

        if not flag_enabled:
            return False

        if not allowed_users and not allowed_groups:
            return True

        allowed_group = bool(set(groups) & allowed_groups)
        # Alternative:
        # allowed_group = any(group in allowed_groups for group in groups)

        return user in allowed_users or allowed_group


def main():
    evaluator = FeatureFlagEvaluator()

    evaluator.add_flag("new_checkout", True)
    evaluator.add_flag(
        "beta_dashboard",
        True,
        allowed_users=["alice"],
        allowed_groups=["staff", "beta"],
    )
    evaluator.add_flag("old_feature", False)

    test_cases = [
        ("new_checkout", "bob", [], True),
        ("beta_dashboard", "alice", [], True),
        ("beta_dashboard", "bob", ["beta"], True),
        ("beta_dashboard", "charlie", ["free"], False),
        ("old_feature", "alice", ["staff"], False),
        ("missing_flag", "alice", ["staff"], False),
    ]

    for flag_name, user, groups, expected in test_cases:
        actual = evaluator.is_enabled(flag_name, user, groups)
        assert actual == expected, (
            f"Failed for flag={flag_name}, user={user}, groups={groups}. "
            f"Expected {expected}, got {actual}."
        )

    print("All tests passed.")


if __name__ == "__main__":
    main()