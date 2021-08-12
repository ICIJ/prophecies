import { find, isMatch, map, trim, uniqueId } from 'lodash'

export default {
  methods: {
    getTaskFilters (task) {
      return {
        predictedValues: {
          param: 'task_record__predicted_value__iregex',
          options: task.choiceGroup.alternativeValues,
          field: 'value'
        },
        assignedTo: {
          param: 'task_record__reviews__checker__in',
          options: task.checkers,
          field: 'id'
        },
        reviewedBy: {
          param: '',
          options: task.checkers,
          field: 'id'
        },
        choices: {
          param: 'choice__in',
          options: task.choiceGroup.choices,
          field: 'id'
        }
      }
    },
    getSelectedFiltersAsQueryParams (filters, selected = {}) {
      return Object.entries(filters).reduce((params, [filter, { field, param }]) => {
        const selected = this.selected[filter] || []
        if (selected.length) {
          if (param.endsWith('__iregex') || param.endsWith('__regex')) {
            const values = map(selected, field).join('|')
            params[`filter[${param}]`] = `(${values})`
          } else {
            params[`filter[${param}]`] = map(selected, field).join(',')
          }
        }
        return params
      }, {})
    },
    mapRouteQueryToFilterOptions (queryParams, task) {
      const filters = this.getTaskFilters(task)
      return Object.entries(queryParams).map(([param, value]) => {
        const [key, filter] = this.findFilterEntry(filters, { param })
        // This will look for existing options in the filters
        const options = this.toValuesList(param, value).map(value => {
          const option = find(filter.options, { [filter.field]: value })
          return option || this.toSerializableOption(value)
        })
        return [key, options]
      })
    },
    findFilterEntry (filters, source) {
      const entries = Object.entries(filters)
      return find(entries, ([key, f]) => isMatch(f, source)) || [null, null]
    },
    toSerializableOption (value) {
      const id = uniqueId('arbitrary-')
      const name = value
      return { id, name, value }
    },
    toValuesList (param, value) {
      if (param.endsWith('__iregex') || param.endsWith('__regex')) {
        return trim(value, '()').split('|')
      }
      return value.split(',')
    }
  }
}
