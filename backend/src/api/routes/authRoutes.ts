import { FastifyPluginAsync } from "fastify";

const authRoutes: FastifyPluginAsync = async function (fastify) {
    fastify.post('/login', async function login(request, reply) {
        const { username, password } = request.body as { username: string, password: string };
        
        if (username === process.env.ADMIN_USERNAME && password === process.env.ADMIN_PASSWORD) {
        
            const token = fastify.jwt.sign({ user: username });
            return reply.status(200).send({
                success: true,
                message: 'Login successful',
                token
            });
        
        } else {
        
            return reply.status(401).send({
                success: false,
                message: 'Invalid username or password'
            })
        
        }
    })
}

export default authRoutes;