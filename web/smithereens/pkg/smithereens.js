export { initSync }
export default __wbg_init;

import * as wasm from "./smithereens/pkg/smithereens_bg.wasm?";
import { __wbg_set_wasm } from "./smithereens/pkg/smithereens_bg.js";
__wbg_set_wasm(wasm);
export * from "./smithereens/pkg/smithereens_bg.js";
