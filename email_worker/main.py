from src.adapters.rabbit import RMQ
from src.adapters.smtp import SmtpWorker
from src.adapters.ws import WS
from src.core.config import settings

import asyncio
from aio_pika.abc import AbstractIncomingMessage
from websockets.server import serve


async def main():
    rabbit = RMQ()
    smtp = SmtpWorker(
        settings.smtp_address,
        settings.smtp_port,
        settings.smtp_login,
        settings.smtp_password,
        settings.smtp_use_tls
    )
    ws = WS()

    await rabbit.connect(settings.get_amqp_uri(), queue_name="email_worker")

    await rabbit.consume_queue(func=smtp.send_likes, binding_keys="event.like", task_id=1)
    await rabbit.consume_queue(func=smtp.send_new_series, binding_keys="event.series", task_id=2)
    await rabbit.consume_queue(func=smtp.send_verify, binding_keys="event.verify", task_id=3)

    async with (
        rabbit.queue.iterator() as iterator,
        serve(ws.register, settings.ws_host, settings.ws_port)
    ):
        message: AbstractIncomingMessage
        async for message in iterator:
            async with message.process(ignore_processed=True):
                body: dict = rabbit._deserialize(message.body)
                task_id = body.pop("task_id")
                await rabbit.funcs[task_id](message)

    # await rabbit.start_iterator()


if __name__ == "__main__":
    asyncio.run(main())
