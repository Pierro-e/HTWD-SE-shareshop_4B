import PopUp from "./PopUp.vue";
import { render } from "@testing-library/vue";
import { describe, it, expect, test } from "vitest";

describe("PopUp", () => {
  it("der Default-Name ist PopUp", () => {
    const { getByRole } = render(PopUp, {});
    const button = getByRole("button");
  });

  test("should work", ({ task }) => {
    console.log(task.name);
  });

  test("math is easy", ({ task }) => {
    console.log(task.name);
    expect(2 + 7).toBe(9);
  });
});
