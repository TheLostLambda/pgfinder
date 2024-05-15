<<<<<<< HEAD
/* tslint:disable */
/* eslint-disable */
/**
* @param {Peptidoglycan} precursor
* @returns {string}
*/
export function pg_to_fragments(precursor: Peptidoglycan): string;
/**
*/
export class Peptidoglycan {
  free(): void;
/**
* @param {string} structure
*/
  constructor(structure: string);
/**
* @returns {string}
*/
  monoisotopic_mass(): string;
}

export type InitInput = RequestInfo | URL | Response | BufferSource | WebAssembly.Module;

export interface InitOutput {
  readonly memory: WebAssembly.Memory;
  readonly __wbg_peptidoglycan_free: (a: number) => void;
  readonly peptidoglycan_new: (a: number, b: number, c: number) => void;
  readonly peptidoglycan_monoisotopic_mass: (a: number, b: number) => void;
  readonly pg_to_fragments: (a: number, b: number) => void;
  readonly __wbindgen_add_to_stack_pointer: (a: number) => number;
  readonly __wbindgen_malloc: (a: number, b: number) => number;
  readonly __wbindgen_realloc: (a: number, b: number, c: number, d: number) => number;
  readonly __wbindgen_free: (a: number, b: number, c: number) => void;
  readonly __wbindgen_exn_store: (a: number) => void;
}

export type SyncInitInput = BufferSource | WebAssembly.Module;
/**
* Instantiates the given `module`, which can either be bytes or
* a precompiled `WebAssembly.Module`.
*
* @param {SyncInitInput} module
*
* @returns {InitOutput}
*/
export function initSync(module: SyncInitInput): InitOutput;

/**
* If `module_or_path` is {RequestInfo} or {URL}, makes a request and
* for everything else, calls `WebAssembly.instantiate` directly.
*
* @param {InitInput | Promise<InitInput>} module_or_path
*
* @returns {Promise<InitOutput>}
*/
export default function __wbg_init (module_or_path?: InitInput | Promise<InitInput>): Promise<InitOutput>;
||||||| parent of 5d68736 (Adding & configuring vite-plugin-wasm-pack)
=======
/* tslint:disable */
/* eslint-disable */
/**
* @param {Peptidoglycan} precursor
* @returns {string}
*/
export function pg_to_fragments(precursor: Peptidoglycan): string;
/**
*/
export class Peptidoglycan {
  free(): void;
/**
* @param {string} structure
*/
  constructor(structure: string);
/**
* @returns {string}
*/
  monoisotopic_mass(): string;
}
>>>>>>> 5d68736 (Adding & configuring vite-plugin-wasm-pack)
