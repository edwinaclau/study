  public function beforeAction($event)
    {
        $action = $event->action->id;
        if (isset($this->actions[$action])) {
            $verbs = $this->actions[$action];
        } elseif (isset($this->actions['*'])) {
            $verbs = $this->actions['*'];
        } else {
            return $event->isValid;
        }

        $verb = Yii::$app->getRequest()->getMethod();
        $allowed = array_map('strtoupper', $verbs);
        if (!in_array($verb, $allowed)) {
            $event->isValid = false;
            // http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.7
            Yii::$app->getResponse()->getHeaders()->set('Allow', implode(', ', $allowed));
            throw new MethodNotAllowedHttpException('Method Not Allowed. This url can only handle the following request methods: ' . implode(', ', $allowed) . '.');
        }

        return $event->isValid;
    }
}


http 方法过滤 

   'verbs' => [
 *             'class' => \yii\filters\VerbFilter::className(),
 *             'actions' => [
 *                 'index'  => ['get'],
 *                 'view'   => ['get'],
 *                 'create' => ['get', 'post'],
 *                 'update' => ['get', 'put', 'post'],
 *                 'delete' => ['post', 'delete'],


上面代码和源代码，都很简单就是map 对应关系，*代表正则任意，而映射到数组里面