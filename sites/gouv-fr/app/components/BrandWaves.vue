<script setup lang="ts">
// Waves taken from https://github.com/betagouv/aides-simplifiees-app/blob/93a0636571c090fdb59895197a8ceba55c58bdf6/inertia/components/layout/BrandBackgroundTexture.vue
// The container queries below choose the wave set and its height from the height of the band.
const WAVES_WIDTH = 1920

const waveSets = [
  {
    name: 'small',
    height: 200,
    paths: {
      top: 'M1920 8.86823V200.498H0V8.86823C102.914 19.978 203.227 31.6236 310.978 35.0561C346.89 36.2045 383.222 36.4257 419.365 35.826C491.433 34.6861 565.737 30.1052 635.706 23.7337C746.761 13.4321 856.3 0.497637 973.953 0.518903C1017.75 0.327503 1061.48 1.595 1104.45 4.0747C1199.17 9.51474 1289.66 20.7053 1384.8 27.2299C1593.55 42.172 1724.13 31.9597 1920 8.86823Z',
      middle: 'M1920 83.6278V200.5H0V87.3417C74.5881 93.4705 149.203 99.6291 223.737 105.741C313.85 113.075 400.616 120.051 492.246 122.884C565.033 125.179 638.903 124.54 710.985 120.349C875.564 111.657 1019.84 80.1396 1188.57 77.729C1317.67 75.0927 1440.69 87.9295 1564.85 95.336C1693.7 103.13 1797.35 96.4093 1920 83.6278Z',
      bottom: 'M1920 192.848V200.496H0V182.302C150.91 181.38 298.068 181.992 447.312 175.952C548.451 171.998 649.198 165.118 747.181 156.526C863.71 146.192 974.807 136.814 1094.76 140.756C1286.85 145.517 1446.94 185.33 1633.68 196.428C1668.72 198.514 1704.42 199.584 1739.98 199.609C1800.78 199.75 1862.03 196.386 1920 192.848Z',
    },
  },
  {
    name: 'medium',
    height: 400,
    paths: {
      top: 'M1920 16.8378V400H0V16.8378C102.914 39.1918 203.227 62.6241 310.978 69.5305C346.89 71.8413 383.222 72.2863 419.365 71.0796C491.433 68.786 565.737 59.5688 635.706 46.7487C746.761 26.0207 856.3 -0.00475535 973.953 0.0380356C1017.75 -0.347083 1061.48 2.20326 1104.45 7.19268C1199.17 18.1386 1289.66 40.6552 1384.8 53.7835C1593.55 83.8484 1724.13 63.3002 1920 16.8378Z',
      middle: 'M1920 165.6V400H0V173.087C74.5881 185.442 149.203 197.858 223.737 210.179C313.85 224.964 400.616 239.029 492.246 244.738C565.033 249.366 638.903 248.078 710.985 239.63C875.564 222.105 1019.84 158.568 1188.57 153.708C1317.67 148.393 1440.69 174.272 1564.85 189.203C1693.7 204.916 1797.35 191.367 1920 165.6Z',
      bottom: 'M1920 385.802V400H0V364.555C150.91 362.698 298.068 363.93 447.312 351.763C548.451 343.796 649.198 329.934 747.181 312.624C863.71 291.805 974.807 272.912 1094.76 280.853C1286.85 290.445 1446.94 370.656 1633.68 393.015C1668.72 397.216 1704.42 399.373 1739.98 399.424C1800.78 399.706 1862.03 392.929 1920 385.802Z',
    },
  },
  {
    name: 'large',
    height: 600,
    paths: {
      top: 'M1920 16.4859V600.5H0V16.4859C102.914 37.7089 203.227 59.9557 310.978 66.5128C346.89 68.7066 383.222 69.1291 419.365 67.9834C491.433 65.8059 565.737 57.055 635.706 44.8835C746.761 25.2042 856.3 0.495485 973.953 0.536111C1017.75 0.170477 1061.48 2.59179 1104.45 7.32878C1199.17 17.7209 1289.66 39.0983 1384.8 51.5624C1593.55 80.1063 1724.13 60.5976 1920 16.4859Z',
      middle: 'M1920 272.698V600.303H0V282.027C74.5881 297.422 149.203 312.892 223.737 328.244C313.85 346.666 400.616 364.19 492.246 371.305C565.033 377.071 638.903 375.466 710.985 364.939C875.564 343.104 1019.84 263.936 1188.57 257.881C1317.67 251.259 1440.69 283.503 1564.85 302.108C1693.7 321.686 1797.35 304.804 1920 272.698Z',
      bottom: 'M1920 583.195V600.337H0V557.543C150.91 555.301 298.068 556.789 447.312 542.099C548.451 532.481 649.198 515.745 747.182 494.845C863.71 469.71 974.807 446.9 1094.76 456.487C1286.85 468.068 1446.94 564.909 1633.68 591.904C1668.72 596.976 1704.42 599.579 1739.98 599.641C1800.78 599.982 1862.03 591.8 1920 583.195Z',
    },
  },
  {
    name: 'xlarge',
    height: 800,
    paths: {
      top: 'M1920 25.0303V800H0V25.0303C102.914 58.2609 203.227 93.0945 310.978 103.361C346.89 106.796 383.222 107.458 419.365 105.664C491.433 102.254 565.737 88.5526 635.706 69.4947C746.761 38.6813 856.3 -0.0070691 973.953 0.0565422C1017.75 -0.51596 1061.48 3.27527 1104.45 10.6924C1199.17 26.9641 1289.66 60.4364 1384.8 79.9524C1593.55 124.646 1724.13 94.0995 1920 25.0303Z',
      middle: 'M1920 337.763V799.999H0V349.613C74.5881 369.167 149.203 388.817 223.737 408.317C313.85 431.717 400.616 453.976 492.246 463.013C565.033 470.337 638.903 468.299 710.985 454.927C875.564 427.192 1019.84 326.634 1188.57 318.942C1317.67 310.531 1440.69 351.488 1564.85 375.119C1693.7 399.987 1797.35 378.544 1920 337.763Z',
      bottom: 'M1920 778.988V799.999H0V748.091C150.91 745.391 298.068 747.183 447.312 729.488C548.451 717.903 649.198 697.744 747.181 672.57C863.71 642.295 974.807 614.819 1094.76 626.367C1286.85 640.316 1446.94 756.963 1633.68 789.478C1668.72 795.588 1704.42 798.724 1739.98 798.799C1800.78 799.209 1862.03 789.354 1920 778.988Z',
    },
  },
]
</script>

<template>
  <div
    class="waves"
    aria-hidden="true"
  >
    <div class="waves-layout">
      <div class="waves-fill" />
      <svg
        v-for="waveSet in waveSets"
        :key="waveSet.name"
        class="waves-svg"
        :class="`waves-svg--${waveSet.name}`"
        :height="waveSet.height"
        :viewBox="`0 0 ${WAVES_WIDTH} ${waveSet.height}`"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          v-for="(path, position) in waveSet.paths"
          :key="position"
          :class="`wave-${position}`"
          :d="path"
        />
      </svg>
      <div class="waves-fill waves-fill--bottom" />
    </div>
    <div class="waves-overlay" />
  </div>
</template>

<style scoped>
.waves {
  --wave-bottom: #b3b3f9;
  /* share of the gap between the band width and the drawing width that the drawing keeps: 0 stretches the drawing to the band, 1 keeps its width */
  --crop-ratio: 0.3;

  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  width: calc(100% + (v-bind(WAVES_WIDTH) * 1px - 100%) * var(--crop-ratio));
  container-type: size;
}

.waves-layout,
.waves-overlay {
  display: none;
}

@container (height > 50px) {
  .waves-layout {
    display: flex;
    flex-direction: column;
    height: 100%;
    background: var(--grey-1000-50);
  }

  .waves-overlay {
    display: block;
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, var(--grey-1000-50) 10%, transparent 100%);
  }
}

.waves-fill {
  flex: none;
  height: 25px;
}

.waves-fill--bottom {
  background: var(--wave-bottom);
}

.waves-svg {
  display: none;
  flex: none;
  width: 100%;
}

.waves-svg--small {
  display: block;
  height: calc(100cqb - 50px);
}

@container (height > 250px) {
  .waves-fill {
    flex: 1;
  }

  .waves-svg--small {
    height: 200px;
  }
}

@container (height > 500px) {
  .waves-svg--small {
    display: none;
  }

  .waves-svg--medium {
    display: block;
  }
}

@container (height > 1000px) {
  .waves-svg--medium {
    display: none;
  }

  .waves-svg--large {
    display: block;
  }
}

@container (height > 1500px) {
  .waves-svg--large {
    display: none;
  }

  .waves-svg--xlarge {
    display: block;
  }
}

.wave-top {
  fill: var(--blue-france-925-125);
}

.wave-middle {
  fill: var(--blue-france-850-200);
}

.wave-bottom {
  fill: var(--wave-bottom);
}
</style>
