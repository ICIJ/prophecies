import { find, isMatch, map, range, trim, uniqueId } from 'lodash'

export default {
  methods: {
    getTaskFilters (task) {
      return !task ? {} : {
        predictedValues: {
          allowArbitraryOptions: true,
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
          name: 'Classification',
          param: 'choice__in',
          nullParam: 'choice__isnull',
          nullValue: true,
          options: [
            ...task.choiceGroup.choices,
            { id: '-1', name: 'Not classified yet' }
          ],
          field: 'id',
          label: 'name'
        },
        priorities: {
          name: 'Priority',
          param: 'task_record__priority__in',
          field: 'label',
          label: 'name',
          options: range(1, 4).map(String).map(label => {
            const name = `Priority ${label}`
            return { label, name }
          })
        },
        rounds: {
          name: 'Rounds',
          param: 'task_record__rounds__in',
          field: 'label',
          label: 'name',
          options: range(1, task.rounds + 1).map(String).map(label => {
            const name = `Round ${label}`
            return { label, name }
          })
        },
        hasDisagreements: {
          name: 'Disagreements',
          param: 'task_record__has_disagreements',
          label: 'name',
          field: 'value',
          options: [
            { value: '1', label: 'Yes', name: 'Disagree' },
            { value: '0', label: 'No', name: 'Agree' }
          ]
        },
        locked: {
          name: 'Locked',
          param: 'task_record__locked',
          label: 'name',
          field: 'value',
          options: [
            { value: '1', label: 'Yes', name: 'Locked' },
            { value: '0', label: 'No', name: 'Not locked' }
          ]
        },
        hasNotes: {
          name: 'Notes',
          param: 'task_record__has_notes',
          label: 'name',
          field: 'value',
          options: [
            { value: '1', label: 'Yes', name: 'With notes' },
            { value: '0', label: 'No', name: 'Without notes' }
          ]
        }
      }
    },
    getSelectedFiltersAsRouteFilters (filters, selected = {}) {
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
      return Object.entries(queryParams).map(([queryParam, value]) => {
        const param = this.toFilterParam(queryParam)
        const [key, filter] = this.findFilterEntry(filters, { param })
        const { allowArbitraryOptions } = filter
        // This will look for existing options in the filters
        const options = this.toValuesList(param, value).map(value => {
          const option = find(filter.options, { [filter.field]: value })
          return option || this.toSerializableOption(value, allowArbitraryOptions)
        })
        return [key, options]
      })
    },
    mapRouteFiltersToAppliedQueryParams (routeFilters, task) {
      const filters = this.getTaskFilters(task)
      return Object.entries(routeFilters).reduce((all, [queryParam, value]) => {
        const param = this.toFilterParam(queryParam)
        const [, filter] = this.findFilterEntry(filters, { param })
        if (this.useNullParam(filter, value)) {
          const nullValue = filter.nullValue === undefined ? '-1' : filter.nullValue
          all[this.toQueryParam(filter.nullParam)] = nullValue
          all[this.toQueryParam(filter.param)] = this.withoutNullValue(filter, value)
        } else {
          all[this.toQueryParam(filter.param)] = value
        }
        return all
      }, {})
    },
    useNullParam (filter, value) {
      const values = this.toValuesList(filter.param, value)
      return values.includes('-1') && filter.nullParam
    },
    withoutNullValue (filter, value) {
      const values = this.toValuesList(filter.param, value).filter(v => v !== '-1')
      return values.length ? this.toValuesParam(filter.param, values) : null
    },
    findFilterEntry (filters, source) {
      const entries = Object.entries(filters)
      return find(entries, ([key, f]) => isMatch(f, source)) || [null, null]
    },
    toSerializableOption (value, allowArbitraryOptions = false) {
      const id = allowArbitraryOptions ? uniqueId('arbitrary-') : -1
      const name = value
      return { id, name, value }
    },
    toValuesList (param, value) {
      if (param.endsWith('__iregex') || param.endsWith('__regex')) {
        return trim(value, '()').split('|')
      }
      return value.split(',')
    },
    toValuesParam (param, values) {
      if (param.endsWith('__iregex') || param.endsWith('__regex')) {
        return `(${values.join('|')})`
      }
      return values.join(',')
    },
    toFilterParam (key) {
      return key.split('filter[').pop().split(']').shift()
    },
    toQueryParam (param) {
      param = this.toFilterParam(param)
      return `filter[${param}]`
    },
    isFiltersParam (filters, { key }) {
      const param = this.toFilterParam(key)
      const entry = this.findFilterEntry(filters, { param })
      return !!entry[0]
    }
  }
}
