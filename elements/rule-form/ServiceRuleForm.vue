<script setup lang="ts">
import UiRuleForm from '@datagouv/regles-site-gouv-fr/app/components/UiRuleForm.vue'
import { serviceCalculator } from '#layers/web/calculation/calculator'

const props = defineProps<{
  // identifier of the record, which is also the identifier of the rule in the calculation service
  rule: string
  service: string
}>()

const calculator = serviceCalculator(props.service, props.rule)
</script>

<template>
  <UiRuleForm :calculator="calculator" />
</template>
