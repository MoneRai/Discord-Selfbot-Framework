from inspect import signature, _empty, _ParameterKind

def parse_args(string: str, coro):
    args = []
    pos = False
    if len(tuple(signature(coro).parameters.items())) >= 2:
        for i, (elem, param) in tuple(enumerate(zip(string.split(), tuple(signature(coro).parameters.items())[1:]))):
            if param[1].annotation != _empty and param[1].annotation:
                args.append(param[1].annotation().__class__(elem))
            elif param[1].kind == _ParameterKind.VAR_POSITIONAL:
                args.append(string.split()[i:])
                pos = True
            else:
                args.append(elem)
        else:
            if len(args) != len(tuple(signature(coro).parameters.items())) - 1 or (len(args) != len(string.split()) and not pos):
                raise ValueError("Different dimensions")
    return args