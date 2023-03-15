import moment from 'moment'

export function formatDateLongAlt (d) {
  return moment(d).format('ddd DD, MMM YYYY - h:MMa')
}

export function formatDateLong (d) {
  return moment(d).format('MMM Do YYYY - hh:mm')
}

export function formatDate (d) {
  return moment(d).format('ddd DD, MMM YYYY')
}

export function formatDateFromNow (d) {
  return moment(d).fromNow()
}
