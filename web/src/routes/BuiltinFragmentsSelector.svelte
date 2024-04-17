<script lang="ts">
	import { Accordion, AccordionItem, ListBox, ListBoxItem } from '@skeletonlabs/skeleton';
	import Tooltip from './Tooltip.svelte';
	export let value: VirtFile | undefined;
	export let fragmentsLibraries: FragmentsLibraryIndex;
</script>

{#each Object.entries(fragmentsLibraries) as [speciesFragments, librariesFragments], speciesIdFragments}
    <label>
      <div class="flex items-center">
        <input
          type="radio"
          name="fragments-library"
        />
        <p class="grow"><i>{speciesFragments}</i></p>
        <Tooltip popupId="library{speciesIdFragments}">
          {librariesFragments['Description']}
        </Tooltip>
      </div>
    </label>
{/each}
