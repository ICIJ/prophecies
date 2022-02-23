import Task from '@/models/Task'
import Action from '@/models/Action'
import ActionAggregate from '@/models/ActionAggregate'
import Tip from '@/models/Tip'

const getIds = (object) => {
  const { response: { data: { data: arr } } } = object
  return arr.map(o => o.id)
}

const USER_FILTER_ATTR = {
  Task: 'checkers',
  ActionAggregate: 'user',
  Tip: 'creator'
}
const userFilterParam = (model, userId) => {
  const filterName = `filter[${[USER_FILTER_ATTR[model.entity]]}]`
  return userId ? { [filterName]: userId } : undefined
}

const filterActorTargetCb = (userId, { response: { data: { data: actions } } }) => {
  if (userId) {
    actions = actions.filter(({ relationships: { actor, target } }) =>
      (actor.data.id === userId || target.data.id === userId))
  }
  return actions.map(action => action.id)
}

export const fetchHistoryItemsIds = async (userId) => {
  const [taskIds, actionIds, actionAggregateIds, tipIds] = await Promise.all([
    Task.api().get('', userFilterParam(Task, userId)).then(getIds),
    Action.api().get('', { 'filter[verb]': 'mentioned' }).then(filterActorTargetCb.bind(this, userId)),
    ActionAggregate.api().get('', userFilterParam(ActionAggregate, userId)).then(getIds),
    Tip.api().get('', userFilterParam(Tip, userId)).then(getIds)
  ])

  return { taskIds, actionIds, actionAggregateIds, tipIds }
}
