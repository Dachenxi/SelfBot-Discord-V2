-- CreateTable
CREATE TABLE "Sniff" (
    "id" TEXT NOT NULL,
    "channelId" TEXT NOT NULL,
    "webhookUrl" TEXT NOT NULL,
    "channelName" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Sniff_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "Sniff_channelId_key" ON "Sniff"("channelId");
