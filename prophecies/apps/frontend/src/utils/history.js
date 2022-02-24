import Action from '@/models/Action'
import Task from '@/models/Task'

const getActionIds = (object) => {
  const { entities: { Action: arr } } = object
  return arr.map(o => o.id)
}

export const fetchHistoryItemsIds = async (userId) => {
  const userFilterParam = userId ? { 'filter[user_stream]': userId } : undefined
  const actionParams = {
    'filter[verb__in]': 'mentioned,created,updated,closed,created-aggregate',
    'page[size]': '1000',
    ...userFilterParam
  }

  // TODO MV CD improve by retrieving only task actions. Maybe do the same for users
  await Task.api().get('', { params: { include: 'project' } })

  return Action.api().get('', { params: actionParams }).then(getActionIds)
}
