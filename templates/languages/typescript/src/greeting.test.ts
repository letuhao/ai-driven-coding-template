import { expect, test } from "vitest";
import { greet } from "./greeting.js";

test("greet", () => {
  expect(greet("world")).toBe("Hello, world!");
  expect(greet("")).toBe("Hello, stranger!");
});
