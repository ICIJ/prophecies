import Action from '@/models/Action'
import Task from '@/models/Task'

export const fetchHistoryItemsIds = async (userId, pageSize, pageNumber) => {
  const userFilterParam = userId ? { 'filter[user_stream]': userId } : undefined
  const paginationParam = pageSize ? { 'page[size]': pageSize, 'page[number]': pageNumber } : undefined
  const actionParams = {
    'filter[verb__in]': 'mentioned,created,updated,closed,created-aggregate',
    'page[size]': '1000',
    ...userFilterParam,
    ...paginationParam
  }

  // TODO MV CD improve by retrieving only task actions. Maybe do the same for users
  await Task.api().get('', { params: { include: 'project' } })

  return Action.api().get('', { params: actionParams })
}
