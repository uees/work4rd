import defaultSettings from '@/settings'

const title = defaultSettings.title || 'Rongda ERP'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
