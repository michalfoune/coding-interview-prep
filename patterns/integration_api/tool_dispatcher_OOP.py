"""
Problem: Tool Dispatcher
Pattern: Python OOP + registry / validation / light polymorphism

Prompt:
    Implement a tool dispatcher.

    You can register tools by name. Each tool has:
        - name
        - function
        - required argument names

    Support:
        - register(name, func, required_args)
        - call(name, args)

Rules:
    - If tool name is unknown, raise ValueError.
    - If a required argument is missing, raise ValueError.
    - Otherwise call the registered function.

Distributed-systems / agentic-system idea:
    A router receives tool-call requests, validates them, and dispatches to
    the correct implementation.

Polymorphism hint:
    Different tools can have different implementations, but the dispatcher
    calls them through one common interface:

        func(args)

    This is polymorphic-ish without requiring inheritance.
"""


class ToolDispatcher:
    def __init__(self):
        self.tools = {}

    def register(self, name: str, func, required_args: list[str]) -> None:
        self.tools[name] = {
            "func": func,
            "required_args": required_args,
        }

    def call(self, name: str, args: dict):
        if name not in self.tools:
            raise ValueError(f"Unknown tool: {name}")

        tool = self.tools[name]

        for required_arg in tool["required_args"]:
            if required_arg not in args:
                raise ValueError(f"Missing required argument: {required_arg}")

        func = tool["func"]
        return func(args)


def add(args: dict) -> int:
    return args["a"] + args["b"]


def greet(args: dict) -> str:
    return "Hello " + args["name"]


def main():
    dispatcher = ToolDispatcher()

    dispatcher.register("add", add, ["a", "b"])
    dispatcher.register("greet", greet, ["name"])

    assert dispatcher.call("add", {"a": 2, "b": 3}) == 5
    assert dispatcher.call("greet", {"name": "Michal"}) == "Hello Michal"

    try:
        dispatcher.call("missing_tool", {})
        assert False, "Expected ValueError for unknown tool"
    except ValueError:
        pass

    try:
        dispatcher.call("add", {"a": 2})
        assert False, "Expected ValueError for missing argument"
    except ValueError:
        pass

    print("All tests passed.")


if __name__ == "__main__":
    main()
