import { orderBy } from 'lodash'

import { TaskStatusOrder } from '@/models/Task'

const orderByProjectName = ({ project }) => project?.name || ''
const orderByTaskName = ({ task }) => task?.name || ''

export const orderByProjectThenTask = (items) => {
  return orderBy(items, [orderByProjectName, orderByTaskName])
}

const orderByStatus = (task) => TaskStatusOrder[task.status] === 1
export const orderTasks = (tasks) => {
  return orderBy(tasks, [orderByStatus, 'priority', 'name'])
}
