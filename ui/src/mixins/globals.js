import { DateTime } from 'luxon'
export default {
  methods: {
    dateformat (dt) {
      return DateTime
        .fromISO(dt)
        .toLocaleString(DateTime.DATE_MED)
    },
    datetimeformat (dt) {
      return DateTime
        .fromISO(dt)
        .toLocaleString(DateTime.DATETIME_MED)
    }
  }
}
