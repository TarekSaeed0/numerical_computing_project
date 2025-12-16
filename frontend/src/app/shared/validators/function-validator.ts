import { AbstractControl, ValidationErrors } from "@angular/forms";
import { parse, OperatorNode, SymbolNode, FunctionNode } from "mathjs";

const allowedConstants = new Set(["e", "pi"]);

const allowedFunctions = new Set([
  "sqrt",
  "cbrt",
  "sin",
  "cos",
  "tan",
  "csc",
  "sec",
  "cot",
  "sinh",
  "cosh",
  "tanh",
  "csch",
  "sech",
  "coth",
  "asin",
  "acos",
  "atan",
  "acsc",
  "asec",
  "acot",
  "asinh",
  "acosh",
  "atanh",
  "acsch",
  "asech",
  "acoth",
  "log",
  "exp",
]);

const allowedOperators = new Set(["+", "-", "*", "/", "^"]);

export function functionValidator(
  control: AbstractControl,
): ValidationErrors | null {
  if (!control.value) {
    return null;
  }

  try {
    const node = parse(control.value);

    if (
      node.filter(
        (n) =>
          ![
            "ConstantNode",
            "FunctionNode",
            "OperatorNode",
            "ParenthesisNode",
            "SymbolNode",
          ].includes(n.type),
      ).length > 0
    ) {
      return { invalidFunction: true };
    }

    const operators = node
      .filter((n) => n.type === "OperatorNode")
      .map((n) => (n as OperatorNode).op)
      .filter((op) => !allowedOperators.has(op));

    if (operators.length !== 0) {
      return { invalidFunction: true };
    }

    const functions = node.filter(
      (n, _, p) =>
        n.type === "SymbolNode" &&
        allowedFunctions.has((n as SymbolNode).name) &&
        !(p && p.type === "FunctionNode" && (p as FunctionNode).fn == n),
    );

    if (functions.length !== 0) {
      return { invalidFunction: true };
    }

    const symbols = node
      .filter((n) => n.type === "SymbolNode")
      .map((n) => (n as SymbolNode).name)
      .filter(
        (n) =>
          n !== "x" && !allowedConstants.has(n) && !allowedFunctions.has(n),
      );

    if (symbols.length !== 0) {
      return { invalidFunction: true };
    }

    return null;
  } catch {
    return { invalidFunction: true };
  }
}
