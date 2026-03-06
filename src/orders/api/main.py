"""
FastAPI приложение — точка входа
==================================
Аналогии C# → Python:
  WebApplication.CreateBuilder()  = FastAPI()
  app.UseMiddleware<T>()          = @app.middleware("http")
  app.MapControllers()            = app.include_router(router)
  IHostApplicationLifetime        = lifespan context manager
  app.UseExceptionHandler()       = @app.exception_handler(ExceptionType)
  builder.Services.AddCors()      = app.add_middleware(CORSMiddleware, ...)
"""

import time
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.orders.api.routers.orders import router as orders_router
from src.orders.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Lifecycle хуки приложения.

    C# аналог:
        IHostedService / IHostApplicationLifetime:
            - OnStarted   → код ДО yield
            - OnStopping  → код ПОСЛЕ yield

        или в .NET 8:
            app.Lifetime.ApplicationStarted.Register(() => { ... });
    """
    # Startup
    print(f"🚀 {settings.app_title} v{settings.app_version} запущен")
    print(f"   Среда: {settings.app_env} | Debug: {settings.debug}")

    yield  # приложение работает

    # Shutdown
    print(f"🛑 {settings.app_title} останавливается...")


app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    description="Учебный проект Orders API. Python для .NET разработчика.",
    lifespan=lifespan,
)

# --- CORS Middleware (C#: builder.Services.AddCors()) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else ["https://yourdomain.com"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Timing Middleware (C#: custom IMiddleware) ---
@app.middleware("http")
async def timing_middleware(request: Request, call_next: object) -> Response:
    """
    Добавляет заголовок X-Process-Time к каждому ответу.

    C# аналог:
        public class TimingMiddleware(RequestDelegate next) {
            public async Task InvokeAsync(HttpContext ctx) {
                var sw = Stopwatch.StartNew();
                await next(ctx);
                ctx.Response.Headers["X-Process-Time"] = $"{sw.ElapsedMilliseconds}ms";
            }
        }
    """
    from collections.abc import Callable
    assert callable(call_next)
    start = time.perf_counter()
    response: Response = await call_next(request)  # type: ignore[operator]
    process_time = time.perf_counter() - start
    response.headers["X-Process-Time"] = f"{process_time * 1000:.2f}ms"
    return response


# --- Exception Handler (C#: app.UseExceptionHandler / ProblemDetails) ---
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """
    C# аналог:
        app.UseExceptionHandler(builder => builder.Run(async ctx => {
            if (ctx.Features.Get<IExceptionHandlerFeature>()?.Error is NotFoundException e)
                ctx.Response.StatusCode = 404;
        }));
    """
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "ValueError"},
    )


# --- Роутеры (C#: app.MapControllers()) ---
app.include_router(orders_router, prefix="/api/v1")


# --- Health Check (C#: app.MapHealthChecks("/health")) ---
@app.get("/health", tags=["system"])
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "version": settings.app_version,
        "env": settings.app_env,
    }


@app.get("/", tags=["system"])
async def root() -> dict[str, str]:
    return {
        "message": f"Welcome to {settings.app_title}",
        "docs": "/docs",
        "health": "/health",
    }
