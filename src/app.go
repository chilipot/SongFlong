package src

import (
	"github.com/chilipot/songflong/src/handlers"
	"github.com/chilipot/songflong/src/models"
	"github.com/gin-gonic/gin"
)

type App struct {
	Router  *gin.Engine
	Sources *models.ExternalAPI
}

type RequestHandlerFunction func(api *models.ExternalAPI, context *gin.Context)

func (app *App) initRoutes() *gin.Engine {
	r := gin.Default()

	r.GET("/search", app.handleRequest(handlers.FindTracks))

	r.POST("/job", app.handleRequest(handlers.SubmitJob))

	r.GET("/job/:jobId", app.handleRequest(handlers.GetJob))

	return r
}

func (app *App) Initialize() {
	app.Router = app.initRoutes()
	sources := models.InitializeSources()
	app.Sources = &sources
}

func (app *App) Start() {
	app.Router.Run()
}

func (app *App) handleRequest(handler RequestHandlerFunction) gin.HandlerFunc {
	return func(context *gin.Context) {
		handler(app.Sources, context)
	}
}
