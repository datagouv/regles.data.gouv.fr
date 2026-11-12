import { defineCustomElement } from 'vue'
import ServiceRuleForm from './ServiceRuleForm.vue'
import '@gouvminint/vue-dsfr/styles'
import '@shallowred/jsonforms-vue-dsfr/styles'

// rendered in the light DOM, so that the DSFR stylesheet of the host page applies
customElements.define('rule-form', defineCustomElement(ServiceRuleForm, { shadowRoot: false }))
