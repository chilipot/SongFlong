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
		requestId := uuid.NewV4().String()
		c.Writer.Header().Set("X-Request-Id", requestId)
		c.Set("requestID", requestId)
		log.WithField("requestID", requestId).Info("Handling request")
		c.Next()
	}
}

// Creates a Gin Engine instance with the app's middleware and routes
func (app *App) initRoutes() *gin.Engine {
	r := gin.Default()

	r.Use(RequestIdMiddleware())

	r.GET("/search", app.handleRequest(handlers.FindTracks))

	r.GET("/streams", app.handleRequest(handlers.GetStreams))

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
