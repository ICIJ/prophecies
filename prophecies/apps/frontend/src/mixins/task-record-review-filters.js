import { find, isMatch, map, range, trim, uniqueId } from 'lodash'

export default {
  methods: {
    getTaskFilters (task) {
      return {
        predictedValues: {
          name: 'Predicted value',
          param: 'task_record__predicted_value__iregex',
          options: task.choiceGroup.alternativeValues,
          field: 'value',
          label: 'name'
        },
        assignedTo: {
          name: 'Assigned to',
          param: 'task_record__reviews__checker__in',
          options: task.checkers,
          field: 'id',
          label: 'displayName'
        },
        reviewedBy: {
          name: 'Reviewed by',
          param: '',
          options: task.checkers,
          field: 'id',
          label: 'displayName'
        },
        choices: {
          name: 'Choices',
          param: 'choice__in',
          options: task.choiceGroup.choices,
          field: 'id',
          label: 'name'
        },
        priorities: {
          name: 'Priority',
          param: 'task_record__priority__in',
          field: 'name',
          options: range(1, 4).map(String).map(name => ({ name }))
        },
        rounds: {
          name: 'Rounds',
          param: 'task_record__rounds__in',
          field: 'name',
          options: range(1, task.rounds + 1).map(String).map(name => ({ name }))
        }
      }
    },
    getSelectedFiltersAsQueryParams (filters, selected = {}) {
      return Object.entries(filters).reduce((params, [filter, { field, param }]) => {
        const filterSelection = selected[filter] || []
        if (filterSelection.length) {
          if (param.endsWith('__iregex') || param.endsWith('__regex')) {
            const values = map(filterSelection, field).join('|')
            params[`filter[${param}]`] = `(${values})`
          } else {
            params[`filter[${param}]`] = map(filterSelection, field).join(',')
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
