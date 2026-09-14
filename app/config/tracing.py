from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
# docker run --name jaeger  -e COLLECTOR_OTLP_ENABLED=true  -p 16686:16686  -p 4317:4317  jaegertracing/all-in-one:latest
# docker start jaeger
def setup_tracing():

    resource = Resource.create({
        'service.name': 'user-api'
    })

    provider = TracerProvider(
        resource=resource
    )

    exporter = OTLPSpanExporter(
        endpoint="http://localhost:4317",
        insecure=True,
    )

    processor = BatchSpanProcessor(
        exporter
    )

    provider.add_span_processor(
        processor
    )

    trace.set_tracer_provider(
        provider
    )
'''
# f you want to know...	Use
"Why did this error happen?"	📝 Logs
"How many requests are failing?"	📊 Metrics
"Which API is slow?"	📊 Metrics
"Which part of this API is slow?"	🔎 Tracing
"Which database operation is slow?"	🔎 Tracing
"What exactly happened to this user/request?"	📝 Logs + Tracing
"Is my application healthy?"	📊 Metrics
"Which Python function is consuming CPU?"	🔥 Profiling
'''