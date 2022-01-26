export function sortByProjectThenTask (a, b) {
  if (!a.project) { return -1 }
  if (!b.project) { return 1 }
  const projectSort = a.project?.name?.localeCompare(b.project?.name)
  if (projectSort !== 0) {
    return projectSort
  } else {
    if (!a.task) { return -1 }
    if (!b.task) { return 1 }
    return (a.task?.name?.localeCompare(b.task?.name))
  }
}
