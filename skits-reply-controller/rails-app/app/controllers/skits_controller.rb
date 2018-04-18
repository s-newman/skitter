require 'rest-client'
require 'json'

class SkitsController < ActionController::API

    def initialize
        if ENV['NODEHOST'] == nil
            @NODEHOST = "skits-controller:8080"
        else
            @NODEHOST = ENV['NODEHOST'] + ":8080"
        end
        puts "NODEHOST = #@NODEHOST"
    end

    def addSkitReply
        r = RestClient.post "http://#@NODEHOST/addSkitReply", params["skit"].to_json, {content_type: :json, accept: :json}
        render json: r
    end

    def removeSkitReply
        render json: {status: 'SUCCESS', message:'Testing'},status: :ok
    end

    def getSkitReplies
        render json: {status: 'SUCCESS', message:'Testing'},status: :ok
    end
end
