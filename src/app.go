package src

import (
	"github.com/chilipot/songflong/src/handlers"
	"github.com/chilipot/songflong/src/models"
	"github.com/gin-gonic/gin"
	uuid "github.com/satori/go.uuid"
	log "github.com/sirupsen/logrus"
)

type App struct {
	Router  *gin.Engine
	Sources *models.ExternalAPI
}

type RequestHandlerFunction func(api *models.ExternalAPI, context *gin.Context)

func RequestIdMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Writer.Header().Set("X-Request-Id", uuid.NewV4().String())
		c.Set("requestID", c.GetHeader("X-Request-Id"))
		log.WithField("requestID", c.GetHeader("X-Request-Id")).Info("Handling request")
		c.Next()
	}
}

func (app *App) initRoutes() *gin.Engine {
	r := gin.Default()

	r.GET("/search", app.handleRequest(handlers.FindTracks))

	r.GET("/streams", app.handleRequest(handlers.GetStreams))

	r.Use(RequestIdMiddleware())

	return r
}

func (app *App) Initialize() {
	app.Router = app.initRoutes()
	sources := models.InitializeSources()
	app.Sources = &sources
	log.Debug("App successfully initialized")
}

func (app *App) Start() {
	log.Debug("Starting app...")
	app.Router.Run()
}

func (app *App) handleRequest(handler RequestHandlerFunction) gin.HandlerFunc {
	return func(context *gin.Context) {
		handler(app.Sources, context)
	}
}
