FROM ruby:2.3.4

WORKDIR /usr/src/app

COPY ./rails-app .

RUN bundle install

EXPOSE 3000

CMD ["rails", "server"]
