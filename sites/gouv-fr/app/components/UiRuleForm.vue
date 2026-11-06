<script setup lang="ts">
import type { JsonSchema } from '@jsonforms/core'
import type { CalculationResult } from '#layers/web/calculation/results'
import type { CalculationErrorKind, CallContract } from '#layers/web/calculation/service'
import { DsfrAlert, DsfrButton } from '@gouvminint/vue-dsfr'
import { JsonForms } from '@jsonforms/vue'
import { createAjv2020, dsfrI18n, dsfrRenderers } from '@shallowred/jsonforms-vue-dsfr'
import { onMounted, ref } from 'vue'
import { presentResults } from '#layers/web/calculation/results'
import { CalculationError, executeRule, fetchCallContract } from '#layers/web/calculation/service'

const props = defineProps<{
  // identifier of the record, which is also the identifier of the rule in the calculation service
  rule: string
  service: string
}>()

const contract = ref<CallContract | null>(null)
const unavailable = ref(false)

onMounted(async () => {
  try {
    contract.value = await fetchCallContract(props.service, props.rule)
  }
  catch {
    unavailable.value = true
  }
})

const ajv = createAjv2020()
const answers = ref<Record<string, unknown>>({})
const invalid = ref(false)
const validationMode = ref<'ValidateAndHide' | 'ValidateAndShow'>('ValidateAndHide')

function onChange(event: { data: Record<string, unknown>, errors?: unknown[] }) {
  answers.value = event.data
  invalid.value = (event.errors?.length ?? 0) > 0
}

const EXECUTION_ERRORS: Record<CalculationErrorKind, string> = {
  refused: 'Le service de calcul a refusé ces informations. Vérifiez-les puis relancez le calcul.',
  failed: 'La règle ne donne pas de résultat pour ces informations.',
  unavailable: 'Le service qui exécute cette règle ne répond pas. Réessayez plus tard.',
}

const results = ref<CalculationResult[] | null>(null)
const executionError = ref<string | null>(null)
const pending = ref(false)

async function execute() {
  validationMode.value = 'ValidateAndShow'
  if (invalid.value || !contract.value) {
    return
  }
  pending.value = true
  executionError.value = null
  try {
    const output = await executeRule(props.service, props.rule, answers.value)
    results.value = presentResults(contract.value.outputSchema, output)
  }
  catch (error) {
    results.value = null
    executionError.value = EXECUTION_ERRORS[error instanceof CalculationError
      ? error.kind
      : 'unavailable']
  }
  finally {
    pending.value = false
  }
}
</script>

<template>
  <div>
    <DsfrAlert
      v-if="unavailable"
      type="error"
      title="Service de calcul indisponible"
      :description="EXECUTION_ERRORS.unavailable"
    />
    <form
      v-else-if="contract"
      novalidate
      @submit.prevent="execute"
    >
      <JsonForms
        :data="answers"
        :schema="contract.inputSchema as JsonSchema"
        :renderers="dsfrRenderers"
        :ajv="ajv"
        :i18n="dsfrI18n"
        :validation-mode="validationMode"
        @change="onChange"
      />
      <div class="fr-mt-4w">
        <DsfrButton
          type="submit"
          label="Calculer"
          :disabled="pending"
        />
      </div>
    </form>
    <!-- a live region present before the result, so that screen readers announce it -->
    <div role="status">
      <div
        v-if="results"
        class="fr-callout fr-mt-4w"
      >
        <h3 class="fr-callout__title">
          Résultat
        </h3>
        <dl class="fr-callout__text">
          <template
            v-for="result in results"
            :key="result.label"
          >
            <dt>{{ result.label }}</dt>
            <dd class="fr-text--bold fr-ml-0 fr-mb-2w">
              {{ result.value }}
            </dd>
          </template>
        </dl>
      </div>
    </div>
    <DsfrAlert
      v-if="executionError"
      alert
      class="fr-mt-4w"
      type="error"
      title="Le calcul n'a pas abouti"
      :description="executionError"
    />
  </div>
</template>
