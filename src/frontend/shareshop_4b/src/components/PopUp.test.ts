import PopUp from "./PopUp.vue";
import { render } from "vitest-browser-vue";
import { expect, test } from "vitest";

test("Default-Name", async () => {
  const { getByText } = render(PopUp);
  await expect.element(getByText("PopUp")).toBeInTheDocument();
});
