from .common import result, subscribeInterval
from .user import User, getUser
from .bot import Bot, getBot
import time
from .config import configAll as conf
from pydash import get, is_dict

subscribeIntervalText = subscribeInterval()

def userWebhook(event):
  message = get(event, 'body')
  body = get(message, 'body')
  defaultResponse = result('user WebHook replied', 200, {
    'headers': {
      'validation-token': get(event, 'headers.validation-token') or get(event, 'headers.Validation-Token')
    }
  })

  if not is_dict(body):
    print('body not dict')
    return defaultResponse

  userId = get(body, 'extensionId') or get(message, 'ownerId')
  eventType = get(message, 'event')
  user = getUser(userId)
  isRenewEvent = eventType == subscribeIntervalText

  if not isinstance(user, User):
    print('no user')
    return defaultResponse

  if isRenewEvent:
    print('isRenewEvent')
    user.renewWebHooks(event)
    user.refresh()
    return defaultResponse

  else:
    print('dddddd')
    conf.userEventAction(
      user,
      eventType,
      event,
      getBot
    )
    return defaultResponse