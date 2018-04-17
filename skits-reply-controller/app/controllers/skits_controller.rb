class SkitsController < ActionController::API
    def addSkitReply
        render json: {status: 'SUCCESS', message:'Testing'},status: :ok
    end

    def removeSkitReply
        render json: {status: 'SUCCESS', message:'Testing'},status: :ok
    end

    def getSkitReplies
        render json: {status: 'SUCCESS', message:'Testing'},status: :ok
    end
end
