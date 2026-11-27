FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY global.json Directory.Build.props Directory.Packages.props NuGet.Config OrgPilot.slnx ./
COPY src/BackendApi/OrgPilot.BackendApi.csproj src/BackendApi/
COPY src/BackgroundWorker/OrgPilot.BackgroundWorker.csproj src/BackgroundWorker/
COPY src/SchedulerReplay/OrgPilot.SchedulerReplay.csproj src/SchedulerReplay/
COPY src/Foundation/OrgPilot.Foundation.csproj src/Foundation/
COPY src/SchedulerReplay/Acceptance/OrgPilot.Acceptance.csproj src/SchedulerReplay/Acceptance/
RUN dotnet restore OrgPilot.slnx
COPY src/BackendApi/ src/BackendApi/
COPY src/BackgroundWorker/ src/BackgroundWorker/
COPY src/SchedulerReplay/ src/SchedulerReplay/
COPY src/Foundation/ src/Foundation/

FROM build AS api-publish
RUN dotnet publish src/BackendApi/OrgPilot.BackendApi.csproj -c Release --no-restore -o /publish

FROM build AS worker-publish
RUN dotnet publish src/BackgroundWorker/OrgPilot.BackgroundWorker.csproj -c Release --no-restore -o /publish

FROM build AS scheduler-publish
RUN dotnet publish src/SchedulerReplay/OrgPilot.SchedulerReplay.csproj -c Release --no-restore -o /publish

FROM build AS acceptance-publish
RUN dotnet publish src/SchedulerReplay/Acceptance/OrgPilot.Acceptance.csproj -c Release --no-restore -o /publish

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
RUN mkdir /archive && chown "$APP_UID" /archive
USER $APP_UID

FROM runtime AS acceptance
COPY --from=acceptance-publish /publish/ ./
ENTRYPOINT ["dotnet", "OrgPilot.Acceptance.dll"]

FROM runtime AS backend-api
COPY --from=api-publish /publish/ ./
EXPOSE 8080
ENTRYPOINT ["dotnet", "OrgPilot.BackendApi.dll"]

FROM runtime AS background-worker
COPY --from=worker-publish /publish/ ./
ENTRYPOINT ["dotnet", "OrgPilot.BackgroundWorker.dll"]

FROM runtime AS scheduler-replay
COPY --from=scheduler-publish /publish/ ./
ENTRYPOINT ["dotnet", "OrgPilot.SchedulerReplay.dll"]
