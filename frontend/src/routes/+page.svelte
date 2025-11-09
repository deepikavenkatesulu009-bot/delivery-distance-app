<script>
    import { source, destination, unit, apiResult, resultBoth, error, loading, calculate } from '$lib/calculatorStore.js';
    import './+page.css'; 
    import { RingLoader } from 'svelte-loading-spinners';
  </script>
  
  <div class="layout">
  
    <main>
      <div class="container">
        <header class="top">
          <div>
            <h1>Distance Calculator</h1>
            </div>
  
          <div>
            <button class="history-button" on:click={() => (location.href = '/history')}>View Historical Queries</button>
          </div>
        </header>
  
        <section class="card">
          <form on:submit|preventDefault={() => calculate()}>
            <div class="form-grid">
              <div>
                <label class="field-label">Source Address</label>
                <input type="text" placeholder="Input address" bind:value={$source} />
              </div>
  
              <div>
                <label class="field-label">Destination Address</label>
                <input type="text" placeholder="Input address" bind:value={$destination} />
              </div>
  
              <!-- RIGHT COLUMN: Unit + Distance -->
              <div class="right-col">
                <div class="unit-distance-wrap">
                  <!-- Unit -->
                  <div class="unit-section">
                    <label class="field-label">Unit</label>
                    <div class="radio-group unit-radios" role="radiogroup" aria-label="Unit">
                      <label class="radio-row">
                        <input type="radio" name="unit" value="mi" bind:group={$unit} />
                        <span class="radio-label-text">Miles</span>
                      </label>
  
                      <label class="radio-row">
                        <input type="radio" name="unit" value="km" bind:group={$unit} />
                        <span class="radio-label-text">Kilometers</span>
                      </label>
  
                      <label class="radio-row">
                        <input type="radio" name="unit" value="both" bind:group={$unit} />
                        <span class="radio-label-text">Both</span>
                      </label>
                    </div>
                  </div>
  
                  <!-- Distance -->
                  <div class="distance-section">
                    <div class="distance-top-row">
                      <label class="field-label distance-label">Distance</label>
                    </div>
  
                    <div class="distance-values">
                      {#if $resultBoth}
                        {#if $unit === 'mi'}
                          <span class="distance-val">{$resultBoth.distance_mi.toFixed(2)} <span class="unit-abbr">mi</span></span>
                        {:else if $unit === 'km'}
                          <span class="distance-val">{$resultBoth.distance_km.toFixed(2)} <span class="unit-abbr">km</span></span>
                        {:else}
                          <span class="distance-val">{$resultBoth.distance_mi.toFixed(2)} <span class="unit-abbr">mi</span></span>
                          <span class="distance-val distance-km">{$resultBoth.distance_km.toFixed(2)} <span class="unit-abbr">km</span></span>
                        {/if}
                      {:else}
                        <span class="placeholder">—</span>
                      {/if}
                    </div>
                  </div>
                </div>
              </div>
            </div>
  
            <div class="calc-area">
              <button
                class="calc-btn"
                type="button"
                on:click={() => calculate()}
                disabled={$loading || !$source.trim() || !$destination.trim()}
              >
                <span>Calculate Distance</span>
                <span class="calc-icon" aria-hidden="true">
                  <!-- calculator SVG -->
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.95)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
                    <rect x="8" y="6" width="8" height="4"></rect>
                    <line x1="9" y1="14" x2="9" y2="14"></line>
                    <line x1="9" y1="18" x2="9" y2="18"></line>
                    <line x1="12" y1="14" x2="12" y2="14"></line>
                    <line x1="12" y1="18" x2="12" y2="18"></line>
                    <line x1="15" y1="14" x2="15" y2="14"></line>
                    <line x1="15" y1="18" x2="15" y2="18"></line>
                  </svg>
                </span>
              </button>
            </div>
  
            {#if $loading}
              <div class="loader-wrap"><RingLoader color="#0070f3" size="40" /></div>
            {/if}
  
            {#if $error}
              <div class="error">{$error}</div>
            {/if}
  
            {#if $apiResult}
              <div class="result" role="status">
                <p style="margin:0 0 6px 0"><strong>API result:</strong> <small style="color:#666">{$apiResult ? JSON.stringify($apiResult) : ''}</small></p>
                {#if $apiResult && $apiResult.source_coords}
                  <p style="margin:0 0 6px 0"><strong>Source:</strong> {Array.isArray($apiResult.source_coords) ? $apiResult.source_coords.join(', ') : $apiResult.source_coords}</p>
                {/if}
                {#if $apiResult && $apiResult.dest_coords}
                  <p style="margin:0 0 6px 0"><strong>Destination:</strong> {Array.isArray($apiResult.dest_coords) ? $apiResult.dest_coords.join(', ') : $apiResult.dest_coords}</p>
                {/if}
              </div>
            {/if}
          </form>
        </section>
  
        <a class="footer-link" href="/history">View History →</a>
      </div>
    </main>
  </div>
  