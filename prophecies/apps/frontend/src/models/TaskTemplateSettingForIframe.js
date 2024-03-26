import TaskTemplateSetting from '@/models/TaskTemplateSetting'

export default class TaskTemplateSettingForIframe extends TaskTemplateSetting {
  static entity = 'TaskTemplateSettingForIframe'

  static fields() {
    return {
      ...super.fields(),
      maxWidth: this.number(null),
      maxHeight: this.number(null),
      ratio: this.number(null),
      displayOriginalValue: this.boolean(true)
    }
  }
}
