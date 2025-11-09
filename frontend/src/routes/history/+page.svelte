<script>
    import { onMount } from 'svelte';
    import { history, loading, error, loadHistory } from '$lib/historyStore.js';
    import './+page.css'; 
  
    function formatDateSafe(value) {
      if (!value) return '—';
      try {
        const d = new Date(value);
        if (isNaN(d.getTime())) return '—';
        return d.toLocaleString();
      } catch {
        return '—';
      }
    }
  
    onMount(() => {
      loadHistory();
    });
  
    function back() {
      location.href = '/';
    }
  </script>
  
  <div class="layout">
  
    <main>
      <div class="container">
        <header class="top">
          <div>
            <h1>Distance Calculator</h1>
            <p class="subtitle">History of the user's queries.</p>
          </div>
  
          <div>
            <button class="back-button" on:click={back}>Back to Calculator</button>
          </div>
        </header>
  
        <section class="card">
          <h2 class="history-title">Historical Queries</h2>
  
          {#if $loading}
            <div class="no-history">Loading history…</div>
          {:else if $error}
            <div class="error">{$error}</div>
          {:else if $history.length === 0}
            <div class="no-history">No history yet. Try calculating a distance!</div>
          {:else}
            <div class="table-wrap" role="region" aria-label="History table">
              <table>
                <thead>
                  <tr>
                    <th style="width:30%;">Source Address</th>
                    <th style="width:30%;">Destination Address</th>
                    <th style="width:12%;">Distance (mi)</th>
                    <th style="width:12%;">Distance (km)</th>
                    <th style="width:16%;">Date</th>
                  </tr>
                </thead>
  
                <tbody>
                  {#each $history as item}
                    <tr>
                      <td>{item.source_text}</td>
                      <td>{item.dest_text}</td>
                      <td>{item.distance_mi != null ? item.distance_mi.toFixed(2) : '—'}</td>
                      <td>{item.distance_km != null ? item.distance_km.toFixed(2) : '—'}</td>
                      <td>{formatDateSafe(item.created_at)}</td>
                    </tr>
                  {/each}
                </tbody>
              </table>
            </div>
          {/if}
        </section>
  
        <a class="footer-link" href="/">← Back to Calculator</a>
      </div>
    </main>
  </div>
  