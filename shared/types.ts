export interface BotStatusResponse {
	isReady: boolean;
	user?: string | null;
}

export interface ClientInfoResponse {
	success: true;
	status: 'Online';
	id: string;
	username: string;
	discriminator: string;
	avatar: string | null;
	uptime: number | null;
	ping: number;
	readyAt: string | Date | null;
	serverCount: number;
	userCount: number;
	memory: {
		heapUsedMB: string;
		rssMB: string;
	}
}

export interface ApiErrorResponse {
	success: false;
	message?: string;
	error?: string;
}

export interface SaveSnifferConfigBody {
	channelId: string;
	webhookUrl: string;
}

export interface SnifferConfigResponse {
	id: string;
	channelId: string;
	webhookUrl: string;
	channelName: string;
	createdAt: string | Date;
	updatedAt: string | Date;
}

export interface SaveSnifferConfigResponse {
	success: true;
	message: string;
	data: SnifferConfigResponse;
}

export interface ListSnifferConfigResponse {
	success: true;
	message: string;
	data: SnifferConfigResponse[];
}
